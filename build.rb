#!/usr/bin/env ruby

require 'fileutils'
require 'pathname'
require 'tempfile'

# Name of the subdirectory where PDFs will be generated
PDF_OUTPUT_SUBDIR = 'pdf'

PDF_ENGINE = 'pdflatex'

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

# Helper to provide a natural sorting key by padding integers with leading zeros
def natural_sort_key(filename)
  filename.gsub(/\d+/) { |num| num.rjust(10, '0') }
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
    end
  end

  puts "Creating combined PDF: #{output_pdf}"

  Tempfile.create(['combined', '.md']) do |tmp|
    md_files.each do |file|
      tmp.puts "\n\\newpage\n\n"

      content = File.read(file)
      content = content.sub(/\A---\s*\n.*?\n---\s*\n/m, '') # Remove front matter

      if File.basename(file) == 'index.md'
        # Step 2: Swap the Liquid tags inside index.md with target cross-reference anchors
        link_mapping.each do |rel_path, anchor_id|
          # Matches standard or nested formats: {% link 6.006/fall-2011/lec1.md %}
          content = content.gsub(/\{\%\s*link\s+.*?#{Regexp.escape(rel_path)}\s*\%}/, anchor_id)
        end
      else
        # For non-index files, fall back to clean standard sanitization
        content = sanitize_markdown(File.read(file))
      end

      tmp.puts content
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
end

puts "\nPDF conversion complete!"