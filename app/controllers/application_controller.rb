class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  # protect_from_forgery with: :exception
  include ApplicationHelper 

  def upload_photo
    require 'fileutils'
    # tmp = params[:file].tempfile
    
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
    p.keepalive = Time.now
    p.save!
    # FileUtils.cp tmp.path, file
    render nothing: true, status: 200
  end

  def pick_photos
    @album = params[:album]
    
    @photos = Photo.order(created_at: :desc)
    if @album and @album != 'all'
      @photos = @photos.where(album: @album)
    end

    if params[:video]
      @albums = Photo.video_albums
      @photos = @photos.where(is_photo: false)
      @num_files = @photos.length
      @photos = @photos.paginate(:page=>params[:page],:per_page=>25)
    else
      @albums = Photo.photo_albums
      @photos = @photos.where(is_photo: true)
      @num_files = @photos.length
      @photos = @photos.paginate(:page=>params[:page],:per_page=>100)
    end
    @selected_ids = Photo.selected_ids
    render 'layouts/pick_photos'
  end

  def requested
    @album = params[:album]
    @albums = Photo.albums
    @requested = Photo.requested
    if params[:album]
      @requested = @requested.where(album: params[:album])
    end
    @photos = @requested.where(is_photo: true)
    @videos = @requested.requested.where(is_photo: false)
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

  def delete_photo
    PhotoRequest.where(photo_id: params[:id]).destroy_all
    Photo.find(params[:id]).destroy
    render nothing: true, status: 200
  end

  def cut_video
    @video = Photo.find(params[:id])
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
    redirect_to :pick
  end


end
