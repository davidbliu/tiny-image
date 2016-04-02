class AddKeepalive < ActiveRecord::Migration
  def change
  	add_column :photos, :keepalive, :datetime
  	add_column :photos, :album, :string
  end
end
