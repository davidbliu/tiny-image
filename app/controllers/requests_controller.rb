class RequestsController < ApplicationController

	def table
		@requested = Photo.requested
	end

	def hashes
		render json: Photo.requested.pluck(:phash).uniq
	end
end
