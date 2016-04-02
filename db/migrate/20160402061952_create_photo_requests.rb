class CreatePhotoRequests < ActiveRecord::Migration
  def change
    create_table :photo_requests do |t|
    	t.string :requester
    	t.integer :photo_id
    	t.string :status
      t.timestamps null: false
    end
  end
end
