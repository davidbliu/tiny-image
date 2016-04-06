class RequestsController < ApplicationController

	def table
		@requested = Photo.requested
	end

	def hashes
		render json: Photo.requested.pluck(:phash).uniq
	end

	def request_photo
		r = PhotoRequest.where(
			photo_id: params[:id],
			requester: myEmail)
		if r.length > 0
			r.destroy_all
		else
			r.first_or_create!
		end
		render nothing: true, status: 200
	end

	def index
		@album = params[:album]
		@albums = Photo.albums
		@requested = Photo.requested
		if params[:album]
			@requested = @requested.where(album: params[:album])
		end
		@photos = @requested.where(is_photo: true)
		@videos = @requested.requested.where(is_photo: false)
	end
end
