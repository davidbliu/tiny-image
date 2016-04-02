class Photo < ActiveRecord::Base
	before_destroy :remove_public_file

	def remove_public_file
		puts 'not implemented yet'
	end

	def self.requested
		Photo.where('id IN (?)',
				PhotoRequest.all.pluck(:photo_id))
	end

	def self.unrequested
		if PhotoRequest.all.length == 0
			return Photo.all
		else
			Photo.where('id NOT IN (?)',
				PhotoRequest.all.pluck(:photo_id))
		end
	end
end
