class AddHashToPhoto < ActiveRecord::Migration
  def change
    add_column :photos, :hash, :string
  end
end
