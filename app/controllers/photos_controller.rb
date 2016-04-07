class PhotosController < ApplicationController
	def upload_photo
		require 'fileutils'
		compressed_path = '/hashed/'+params[:file].original_filename
		path = File.join("public",compressed_path)
		File.delete(path) if File.exist?(path)
		File.open(path, "wb") { |f| f.write(params[:file].read) }
		p = Photo.where(
		  compressed_path: compressed_path,
		  phash: params[:hash]).first_or_create!
		p.is_photo = compressed_path.include?('.png')
		p.email = params[:email]
		p.album = params[:album]
		p.original_path = params[:original_path]
		p.original_size = params[:original_size]
		p.compressed_size = params[:compressed_size]
		p.save!
		render nothing: true, status: 200
	end

	def index
		@album = params[:album]
		@photos = Photo.order(created_at: :desc)
		if @album and @album != 'all'
		  @photos = @photos.where(album: @album)
		end
		if params[:video]
		  @albums = Photo.video_albums
		  @photos = @photos.where(is_photo: false)
		  @num_files = @photos.length
		  @photos = @photos.paginate(:page=>params[:page],:per_page=>21)
		else
		  @albums = Photo.photo_albums
		  @photos = @photos.where(is_photo: true)
		  @num_files = @photos.length
		  @photos = @photos.paginate(:page=>params[:page],:per_page=>100)
		end
		@selected_ids = Photo.selected_ids
	end

	def show
		@photo = Photo.find(params[:id])
		if @photo.is_photo
			render 'show_photo', layout: false
		else
			render 'show_video', layout: false
		end
	end

	def delete_photo
		PhotoRequest.where(photo_id: params[:id]).destroy_all
		Photo.find(params[:id]).destroy
		render nothing: true, status: 200
	end

	def empty
		if params[:album]
			w = Photo.where(album: params[:album])
			ids = w.pluck(:id)
			w.destroy_all
			PhotoRequest.where('photo_id in (?)', ids).destroy_all
		else
			Photo.destroy_all
			PhotoRequest.destroy_all
		end
		redirect_to 'index'
	end
end
