class CreatePhotos < ActiveRecord::Migration
  def change
    create_table :photos do |t|
    	t.string :email
    	t.string :original_path
    	t.string :compressed_path
    	t.boolean :is_photo
      t.timestamps null: false
    end
  end
end
