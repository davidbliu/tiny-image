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
      original_path: params[:original_path]).first_or_create!
    p.is_photo = compressed_path.include?('.png')
    p.email = params[:email]
    p.album = params[:album]
    p.keepalive = Time.now
    p.save!
  	FileUtils.cp tmp.path, file
  	render nothing: true, status: 200
  end

  def keepalive
    Photo.where(original_path: params[:original_path]).each do |photo|
      photo.keepalive = Time.now
      photo.save!
    end
    render nothing: true, status: 200
  end

  def pick_photos
    Photo.process
    @photos = Photo.all.where(is_photo: true).order('created_at desc')
      .paginate(:page=>params[:page],:per_page=>100)
    @selected_ids = Photo.selected_ids
    render 'layouts/pick_photos'
  end

  def pick_videos
    Photo.process
    @selected_ids = Photo.selected_ids
    @videos = Photo.all.where(is_photo: false).order('created_at desc')
    .paginate(:page=>params[:page],:per_page=>25)
    render 'layouts/pick_videos'
  end

  def requested
    Photo.process
    @requested = Photo.requested
    @emails = Photo.all.pluck(:email).uniq
    @photos = Photo.requested.where(is_photo: true)
    @videos = Photo.requested.where(is_photo: false)
    render 'layouts/requested'
  end

  def requested_paths
    Photo.process
    requested = Photo.requested.where(email: params[:email])
    render json: requested.map{|x| x.original_path}
  end


  def fulfill
    @requested = Photo.requested #.select{|x| x.email == myEmail}
    render 'layouts/fulfill'
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


def unrequest_photo
    PhotoRequest.where(
      photo_id: params[:id],
      requester: myEmail).destroy_all
    redirect_to :back
  end


  def home
    render 'layouts/home'
  end

  def empty
    Photo.destroy_all
    PhotoRequest.destroy_all
    redirect_to :pick_photos
  end


end
