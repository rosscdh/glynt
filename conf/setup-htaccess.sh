htpasswd -c /home/stard0g101/webapps/cartvine_shoppers/apache2/conf/.mypasswds weareml

echo "managers: weareml" > /home/stard0g101/webapps/cartvine_shoppers/apache2/conf/.mygroups

# Add to httpd.conf

LoadModule auth_basic_module modules/mod_auth_basic.so
LoadModule authn_file_module modules/mod_authn_file.so
LoadModule authz_user_module modules/mod_authz_user.so
LoadModule authz_groupfile_module modules/mod_authz_groupfile.so

<Location "/">
AuthType Basic
AuthName "Under Construction"
AuthUserFile /home/stard0g101/webapps/cartvine_shoppers/apache2/conf/.mypasswds
AuthGroupFile /home/stard0g101/webapps/cartvine_shoppers/apache2/conf/.mygroups
Require group managers
</Location>