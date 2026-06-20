#!/usr/bin/env ruby

require 'fileutils'
require 'pathname'

def convert_markdown_to_pdf(md_file)
  pdf_file = md_file.sub(/\.md$/, '.pdf')
  
  puts "Converting: #{md_file} -> #{pdf_file}"
  
  # Using pandoc to convert markdown to PDF
  system("pandoc '#{md_file}' -o '#{pdf_file}' --pdf-engine=xelatex")
  
  unless $?.success?
    puts "ERROR: Failed to convert #{md_file}"
    return false
  end
  
  true
end

# Find all directories with index.md
Dir.glob('**/index.md').each do |index_file|
  dir = File.dirname(index_file)
  
  puts "\nProcessing directory: #{dir}"
  
  # Convert all markdown files in this directory
  Dir.glob("#{dir}/**/*.md").each do |md_file|
    convert_markdown_to_pdf(md_file)
  end
end

puts "\nPDF conversion complete!"
