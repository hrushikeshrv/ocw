#!/usr/bin/env ruby

require 'fileutils'
require 'pathname'
require 'tempfile'

# Name of the subdirectory where PDFs will be generated
PDF_OUTPUT_SUBDIR = 'pdf'

# Convert a markdown file to a PDF file
def convert_markdown_to_pdf(md_file, base_dir)
  relative_path = Pathname.new(md_file).relative_path_from(Pathname.new(base_dir))
  pdf_file = File.join(base_dir, PDF_OUTPUT_SUBDIR, relative_path.to_s.sub(/\.md$/, '.pdf'))

  FileUtils.mkdir_p(File.dirname(pdf_file))

  puts "Converting: #{md_file} -> #{pdf_file}"

  system("pandoc '#{md_file}' -o '#{pdf_file}' --pdf-engine=xelatex")

  unless $?.success?
    puts "ERROR: Failed to convert #{md_file}"
    return false
  end

  true
end

# Get a list of ordered markdown files in the directory,
# but put index.md first, then sort any .md files in the directory
# alphabetically, then recurse on subdirectories
def ordered_markdown_files(dir)
  files = []

  # index.md first
  index_file = File.join(dir, 'index.md')
  files << index_file if File.exist?(index_file)

  # other .md files in this directory
  Dir.children(dir)
     .select { |f| f.end_with?('.md') && f != 'index.md' }
     .sort
     .each do |f|
       files << File.join(dir, f)
     end

  # recurse into subdirectories
  Dir.children(dir)
     .select { |f| File.directory?(File.join(dir, f)) }
     .sort
     .each do |subdir|
       files.concat(ordered_markdown_files(File.join(dir, subdir)))
     end

  files
end

# Create a single PDF file containing all lecture notes
def create_combined_pdf(base_dir)
  pdf_dir = File.join(base_dir, PDF_OUTPUT_SUBDIR)
  FileUtils.mkdir_p(pdf_dir)

  dirname = File.basename(base_dir)
  output_pdf = File.join(pdf_dir, "#{dirname}.pdf")

  md_files = ordered_markdown_files(base_dir)

  puts "Creating combined PDF: #{output_pdf}"

  Tempfile.create(['combined', '.md']) do |tmp|
    md_files.each do |file|
      relative_name = Pathname.new(file).relative_path_from(Pathname.new(base_dir))

      tmp.puts
      tmp.puts "\\newpage"
      tmp.puts

      content = File.read(file)

      # Remove YAML front matter from non-index.md files
      unless File.basename(file) == 'index.md'
        content = content.sub(/\A---\s*\n.*?\n---\s*\n/m, '')
      end

      tmp.puts content
    end

    tmp.flush

    system("pandoc '#{tmp.path}' -o '#{output_pdf}' --pdf-engine=xelatex")

    unless $?.success?
      puts "ERROR: Failed to create combined PDF for #{base_dir}"
      return false
    end
  end

  true
end

# Find all directories with index.md
Dir.glob('**/index.md').each do |index_file|
  dir = File.dirname(index_file)

  puts "\nProcessing directory: #{dir}"

  # Convert each markdown file individually
  Dir.glob("#{dir}/**/*.md").each do |md_file|
    convert_markdown_to_pdf(md_file, dir)
  end

  # Create a single PDF containing all markdown files
  create_combined_pdf(dir)
end

puts "\nPDF conversion complete!"
