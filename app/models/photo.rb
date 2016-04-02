class Photo < ActiveRecord::Base
	before_destroy :remove_public_file

	def remove_public_file
		puts 'not implemented yet'
	end
end
