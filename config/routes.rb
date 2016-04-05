Rails.application.routes.draw do
  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".
  post 'upload_photo' => 'application#upload_photo'
  post '/upload_compressed' => 'application#upload_compressed'
  post '/keepalive' => 'application#keepalive'
  root 'application#pick_photos'
  post 'request_photo/:id' => 'application#request_photo'
  post 'delete_photo/:id' => 'application#delete_photo'
  get 'cut_video' => 'application#cut_video'
  get 'fulfill' => 'application#fulfill'
  get 'empty' => 'application#empty'

  get 'pick' => 'application#pick_photos'
  # get 'pick_videos' => 'application#pick_videos'
  get 'requested' => 'application#requested'
  get 'requested_paths' => 'application#requested_paths'

  get 'table' => 'requests#table'
  get 'hashes' => 'requests#hashes'
  # You can have the root of your site routed with "root"
  # root 'welcome#index'

  # Example of regular route:
  #   get 'products/:id' => 'catalog#view'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

  # Example resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Example resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Example resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Example resource route with more complex sub-resources:
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', on: :collection
  #     end
  #   end

  # Example resource route with concerns:
  #   concern :toggleable do
  #     post 'toggle'
  #   end
  #   resources :posts, concerns: :toggleable
  #   resources :photos, concerns: :toggleable

  # Example resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end
end
