class RequestsController < ApplicationController

	def table
		@requested = Photo.requested
	end
end
