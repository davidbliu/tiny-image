class AddSizesToPhotos < ActiveRecord::Migration
  def change
    add_column :photos, :original_size, :integer
    add_column :photos, :compressed_size, :integer
  end
end
