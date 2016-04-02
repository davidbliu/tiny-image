class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  # protect_from_forgery with: :exception
  include ApplicationHelper 
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
    @photos = Photo.unrequested.where(is_photo: true)
    @videos = Photo.unrequested.where(is_photo: false)
    @requested = Photo.requested
    @random = Photo.all.map{|x| x.compressed_path}
    render 'layouts/pick'
  end

  def fulfill
    @requested = Photo.requested #.select{|x| x.email == myEmail}
    render 'layouts/fulfill'
  end

  def request_photo
    PhotoRequest.where(
      photo_id: params[:id],
      requester: myEmail).first_or_create!
    redirect_to :back
  end

  def unrequest_photo
    PhotoRequest.where(
      photo_id: params[:id],
      requester: myEmail).destroy_all
    redirect_to :back
  end

  def home
  	render json: 'Hi there'
  end

  def empty
    Photo.destroy_all
    PhotoRequest.destroy_all
    redirect_to :pick
  end


end
