class Photo < ActiveRecord::Base
	before_destroy :remove_public_file

	def self.process
		puts 'nothing here'
		# Photo.where('keepalive < ?', Time.now-15.minutes).destroy_all
	end


	def remove_public_file
		puts 'not implemented yet'
	end

	def self.requested
		Photo.order('created_at desc').where('id IN (?)', PhotoRequest.all.pluck(:photo_id))
	end

	def self.unrequested
		if PhotoRequest.all.length == 0
			return Photo.all
		else
			Photo.where('id NOT IN (?)',
				PhotoRequest.all.pluck(:photo_id))
		end
	end

	def self.selected_ids
		PhotoRequest.all.pluck(:photo_id)
	end
end
