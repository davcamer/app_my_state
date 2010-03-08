# Be sure to restart your server when you modify this file.

# Your secret key for verifying cookie session data integrity.
# If you change this key, all old sessions will become invalid!
# Make sure the secret is at least 30 characters and all random, 
# no regular words or you'll be exposed to dictionary attacks.
ActionController::Base.session = {
  :key         => '_maps_test_session',
  :secret      => 'a54932f27ffdd15c6db7462ba7ace69f54c2fdac77c4c2f538ff7a0c9fe7142ccedb04ba03b52edb858ba406f35283c29354c68547128415d61df104fecc289d'
}

# Use the database for sessions instead of the cookie-based default,
# which shouldn't be used to store highly confidential information
# (create the session table with "rake db:sessions:create")
# ActionController::Base.session_store = :active_record_store
