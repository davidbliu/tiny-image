class AddHashToPhoto < ActiveRecord::Migration
  def change
    add_column :photos, :phash, :string
  end
end
