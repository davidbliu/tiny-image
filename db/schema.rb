# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20160402184151) do

  create_table "photo_requests", force: :cascade do |t|
    t.string   "requester"
    t.integer  "photo_id"
    t.string   "status"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "photos", force: :cascade do |t|
    t.string   "email"
    t.string   "original_path"
    t.string   "compressed_path"
    t.boolean  "is_photo"
    t.datetime "created_at",      null: false
    t.datetime "updated_at",      null: false
    t.datetime "keepalive"
    t.string   "album"
  end

end
