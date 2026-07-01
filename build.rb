#!/usr/bin/env ruby

require 'fileutils'
require 'pathname'
require 'tempfile'

# Name of the subdirectory where PDFs will be generated
PDF_OUTPUT_SUBDIR = 'pdf'

PDF_ENGINE = 'pdflatex'

# Add any directory paths to exclude from the global combined PDF
# Normalization will handle variations like 'algorithms', './algorithms', or 'algorithms/'
GLOBAL_PDF_IGNORED_DIRECTORIES = ['./algorithms']

# Centralized method to execute Pandoc with global configuration parameters
def run_pandoc(input_path, output_path, resource_path)
  system(
    "pandoc",
    input_path,
    "-o",
    output_path,
    "--pdf-engine=#{PDF_ENGINE}",
    "-V", "geometry:margin=1.5in",
    "-V", "fontsize=11pt",
    "-V", "colorlinks=false",               # Set to false so the border shows up
    "-V", "hyperrefoptions=pdfborderstyle={/S/U/W 1}", # /S/U creates an Underline style, /W 1 sets width to 1pt
    "--resource-path=#{resource_path}"
  )
end

# Sanitizes Jekyll/Liquid tags so they don't break compilers
def sanitize_markdown(content)
  # Remove YAML front matter
  content = content.sub(/\A---\s*\n.*?\n---\s*\n/m, '')

  # Convert {% link 6.004/lec1.md %} to just a regular relative path or text
  content.gsub(/\{\%\s*link\s+([^\s\%]+)\s*\%}/) do
    match = $1
    File.basename(match)
  end
end

# Universally converts ANY {% link <path> %} sequence to its local anchor using a provided map
def convert_jekyll_links_to_anchors(content, link_mapping)
  content.gsub(/\{\%\s*link\s+([^\s\%]+)\s*\%}/) do
    raw_link_path = $1.strip
    lookup_key = raw_link_path.sub(/^\.\//, '') # Standardize lookup key format

    # Try full path first, then fall back to baseline file name match
    matched_anchor = link_mapping[lookup_key] || link_mapping[File.basename(lookup_key)]

    matched_anchor ? matched_anchor : "##" # Fallback safely to a neutral marker if completely missing
  end
end

# Generates a standard Pandoc identifier anchor from a header string
# e.g., "# Lecture 11 - Integer Arithmetic" -> "lecture-11---integer-arithmetic"
def generate_pandoc_id(header_text)
  id = header_text.downcase.strip
  id = id.gsub(/[^a-z0-9\s\-]/, '') # Remove punctuation except hyphens/spaces
  id = id.gsub(/\s+/, '-')          # Convert spaces to hyphens
  "##{id}"
end

# Parses a markdown file to extract its main H1 title
def extract_h1_title(file_path)
  File.foreach(file_path) do |line|
    if line.start_with?('# ')
      return line.sub('# ', '').strip
    end
  end
  nil
end

# Helper to provide a natural sorting key by padding integers with leading zeros
def natural_sort_key(filename)
  filename.to_s.gsub(/\d+/) { |num| num.rjust(10, '0') }
end

# Get a list of ordered markdown files in the directory
def ordered_markdown_files(dir)
  files = []

  index_file = File.join(dir, 'index.md')
  files << index_file if File.exist?(index_file)

  # Sort files naturally (lec1, lec2, ..., lec10)
  Dir.children(dir)
     .select { |f| f.end_with?('.md') && f != 'index.md' }
     .sort_by { |f| natural_sort_key(f) }
     .each do |f|
       files << File.join(dir, f)
     end

  # Recurse into subdirectories using natural sorting as well
  Dir.children(dir)
     .select { |f| File.directory?(File.join(dir, f)) }
     .sort_by { |f| natural_sort_key(f) }
     .each do |subdir|
       files.concat(ordered_markdown_files(File.join(dir, subdir)))
     end

  files
end

# Convert a markdown file to a PDF file
def convert_markdown_to_pdf(md_file, base_dir)
  relative_path = Pathname.new(md_file).relative_path_from(Pathname.new(base_dir))
  pdf_file = File.join(base_dir, PDF_OUTPUT_SUBDIR, relative_path.to_s.sub(/\.md$/, '.pdf'))

  FileUtils.mkdir_p(File.dirname(pdf_file))

  puts "Converting: #{md_file} -> #{pdf_file}"

  Tempfile.create(['sanitized', '.md']) do |tmp|
    clean_content = sanitize_markdown(File.read(md_file))
    tmp.puts clean_content
    tmp.flush

    success = run_pandoc(tmp.path, pdf_file, base_dir)

    unless success
      puts "ERROR: Failed to convert #{md_file}"
      puts "Exit status: #{$?.exitstatus}"
      return false
    end
  end

  true
end

# Create a single PDF file containing all lecture notes with internal working links
def create_combined_pdf(base_dir)
  pdf_dir = File.join(base_dir, PDF_OUTPUT_SUBDIR)
  FileUtils.mkdir_p(pdf_dir)

  dirname = File.basename(base_dir)
  output_pdf = File.join(pdf_dir, "#{dirname}.pdf")

  md_files = ordered_markdown_files(base_dir)

  # Step 1: Map all lecture file relative tracks to their generated Pandoc header IDs
  link_mapping = {}
  md_files.each do |file|
    next if File.basename(file) == 'index.md'

    title = extract_h1_title(file)
    if title
      relative_path_from_base = Pathname.new(file).relative_path_from(Pathname.new(base_dir)).to_s
      link_mapping[relative_path_from_base] = generate_pandoc_id(title)
      link_mapping[File.basename(file)] = generate_pandoc_id(title)
    end
  end

  puts "Creating combined PDF: #{output_pdf}"

  Tempfile.create(['combined', '.md']) do |tmp|
    md_files.each do |file|
      tmp.puts "\n\\newpage\n\n"

      content = File.read(file)
      content = content.sub(/\A---\s*\n.*?\n---\s*\n/m, '') # Remove front matter

      # Convert Jekyll links using the separate refactored method
      content = convert_jekyll_links_to_anchors(content, link_mapping)

      # Shift header depths dynamically while safely preserving trailing spacing
      is_course_index = (File.basename(file) == 'index.md')
      if is_course_index
        content = content.gsub(/^(#+)(\s+)/) { "#{$1}##{$2}" }
      else
        content = content.gsub(/^(#+)(\s+)/) { "#{$1}###{$2}" }
      end

      # Run remaining standalone cleanups for normal Liquid tags
      clean_content = sanitize_markdown(content)
      tmp.puts clean_content
    end

    tmp.flush

    success = run_pandoc(tmp.path, output_pdf, base_dir)

    unless success
      puts "ERROR: Failed to create combined PDF for #{base_dir}"
      puts "Exit status: #{$?.exitstatus}"
      return false
    end
  end

  true
end

# Compile every markdown file across all subdirectories into a single large PDF
def create_global_combined_pdf
  root_pdf_dir = File.join('.', PDF_OUTPUT_SUBDIR)
  FileUtils.mkdir_p(root_pdf_dir)
  output_pdf = File.join(root_pdf_dir, "OCW.pdf")

  # Normalize the ignore list into clean, standardized paths for strict matching
  normalized_ignored = GLOBAL_PDF_IGNORED_DIRECTORIES.map { |d| Pathname.new(d).cleanpath.to_s }

  puts "\nGenerating master comprehensive PDF across all modules: #{output_pdf}"

  # Discover all modules containing index files, excluding the root directory
  module_dirs = Dir.glob('**/index.md')
                   .map { |f| File.dirname(f) }
                   .select { |d| d != '.' && !d.empty? }
                   # Reject any directories that match normalized ignore list
                   .reject { |d| normalized_ignored.include?(Pathname.new(d).cleanpath.to_s) }
                   .sort_by { |d| natural_sort_key(d) }

  all_md_files = []

  # Prepend the project root's index.md if it exists
  root_index = './index.md'
  if File.exist?(root_index)
    all_md_files << root_index
  end

  # Gather files from the rest of the valid subdirectories
  module_dirs.each do |dir|
    all_md_files.concat(ordered_markdown_files(dir))
  end

  if all_md_files.empty?
    puts "No module markdown files found to aggregate."
    return false
  end

  # Build a global mapping of all lecture files to anchor IDs
  global_link_mapping = {}
  all_md_files.each do |file|
    next if File.basename(file) == 'index.md' # Skip index structures

    title = extract_h1_title(file)
    if title
      anchor_id = generate_pandoc_id(title)

      # Map the full relative track (e.g., "6.006/fall-2011/lec1.md")
      global_link_mapping[file.sub(/^\.\//, '')] = anchor_id

      # Also map just the filename base (e.g., "lec1.md") for flexibility
      global_link_mapping[File.basename(file)] = anchor_id
    end
  end

  Tempfile.create(['global_combined', '.md']) do |tmp|
    # Include the current directory '.' as part of the resource search path for assets
    resource_paths = (['.'] + module_dirs).join(File::PATH_SEPARATOR)

    all_md_files.each do |file|
      tmp.puts "\n\\newpage\n\n"

      content = File.read(file)
      content = content.sub(/\A---\s*\n.*?\n---\s*\n/m, '') # Remove front matter

      # Convert Jekyll links via the refactored centralized method
      content = convert_jekyll_links_to_anchors(content, global_link_mapping)

      # Shift header depths dynamically while safely preserving trailing spacing
      is_root_index = (file == root_index)
      is_course_index = (File.basename(file) == 'index.md' && !is_root_index)
      is_lecture_file = (!is_root_index && !is_course_index)

      # For the global combined PDF we want each course to appear as a top-level
      # heading (not nested under the root "Course List"). Therefore, do NOT
      # increase header depth for course index files — leave their headers as-is
      # so the course title remains an H1. Lecture files still get their headers
      # shifted down to remain nested under their course.
      if is_lecture_file
        content = content.gsub(/^(#+)(\s+)/) { "#{$1}###{$2}" }
      end

      # Run remaining standalone cleanups for normal Liquid tags
      clean_content = sanitize_markdown(content)
      tmp.puts clean_content
    end

    tmp.flush

    success = run_pandoc(tmp.path, output_pdf, resource_paths)

    unless success
      puts "ERROR: Failed to create global master PDF"
      puts "Exit status: #{$?.exitstatus}"
      return false
    end
  end

  puts "Master PDF built successfully at #{output_pdf}!"
  true
end

# Check if a specific file path was passed via command line arguments
target_file = ARGV[0]

if target_file
  # --- Single File Test Mode ---
  unless File.exist?(target_file)
    puts "ERROR: File not found: #{target_file}"
    exit 1
  end

  current_dir = File.dirname(target_file)
  until current_dir == '.' || File.exist?(File.join(current_dir, 'index.md'))
    parent = File.dirname(current_dir)
    break if parent == current_dir
    current_dir = parent
  end

  base_dir = current_dir == '.' ? File.dirname(target_file) : current_dir

  puts "Running single-file test mode..."
  convert_markdown_to_pdf(target_file, base_dir)
else
  # --- Standard Batch Processing Mode ---
  Dir.glob('**/index.md').each do |index_file|
    dir = File.dirname(index_file)

    next if dir == '.' || dir.empty?

    puts "\nProcessing directory: #{dir}"

    Dir.glob("#{dir}/**/*.md")
       .sort_by { |f| natural_sort_key(f) }
       .each do |md_file|
         convert_markdown_to_pdf(md_file, dir)
       end

    create_combined_pdf(dir)
  end

  # Build the master combined PDF from all modules
  create_global_combined_pdf
end

puts "\nPDF conversion complete!"