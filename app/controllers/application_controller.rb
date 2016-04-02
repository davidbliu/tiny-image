class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  # protect_from_forgery with: :exception

  def upload_compressed
  	require 'fileutils'
  	tmp = params[:file].tempfile
  	file = File.join("public", "compressed/"+params[:file].original_filename)
    compressed_path = '/compressed/'+params[:file].original_filename
    p = Photo.where(
      compressed_path: compressed_path,
      email: params[:email]).first_or_create!
    p.original_path = params[:original_path]
    p.is_photo = compressed_path.include?('.png')
    p.save!
  	FileUtils.cp tmp.path, file
  	render nothing: true, status: 200
  end

  def pick 
    @photos = Photo.where(is_photo: true)
    @videos = Photo.where(is_photo: false)
    render 'layouts/pick'
  end


  def home
  	render json: 'Hi there'
  end
end
