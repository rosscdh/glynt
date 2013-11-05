/*
 * Embedded Signing - Beta
 * 
 * Here are the detail and steps to setup embedded signing on your site.
 * More general information about the API is available at http://www.hellosign.com/api/gettingStarted
 *
 * /

1. Sign up for an API plan at https://www.hellosign.com/api/pricing (if necessary)
Using embedded signing requires to be on the Silver or Gold plan. Otherwise you can only use it in test mode.

2. Create an API app at https://www.hellosign.com/oauth/createAppForm
Choose your callback urls carefully as they must be in the same domain and embedded signing will only be possible on pages from that same domain

3. On the server side

3.1. Make a request to the API to create an embedded signature request
curl -u"EMAIL_ADDRESS:PASSWORD" https://api.hellosign.com/v3/signature_request/create_embedded_with_reusable_form \
     -F"client_id=YOUR_APP_CLIENT_ID" \
     -F"reusable_form_id=REUSABLE_FORM_ID" \
     -F"subject=My First embedded signature request with a reusable form" \
     -F"message=Isn't it cool" \
     -F"signers[ROLE_NAME][name]=John Doe" \
     -F"signers[ROLE_NAME][email_address]=john.doe@domain.com"
The response will contain a list of signature request with using ids

Alternatively you can do it without using a template:
curl -u"EMAIL_ADDRESS:PASSWORD" https://api.hellosign.com/v3/signature_request/create_embedded \
     -F"client_id=YOUR_APP_CLIENT_ID" \
     -F"file[0]=@FILE_PATH" \
     -F"file[1]=@ANOTHER_FILE_PATH" \
     -F"subject=My First embedded signature request" \
     -F"message=Isn't it cool" \
     -F"signers[0][name]=John Doe" \
     -F"signers[0][email_address]=john.doe@domain.com"

3.2. Fetch the associated signature url for the signer that you need
curl -u"EMAIL_ADDRESS:PASSWORD" https://api.hellosign.com/v3/embedded/sign_url/SIGNATURE_ID
The response will look like { "embedded": { "sign_url": "SIGNATURE_URL", "expires_at": "1382730006" } }

4. On the client side

4.1. Include https://s3.amazonaws.com/cdn.hellofax.com/js/embedded.js on your page

4.2. Use our javascript library to open the signature page in an iFrame
Example:
HelloSign.init('YOUR_APP_CLIENT_ID');
HelloSign.open({
    url: "SIGNATURE_URL",                           // Signature url your fetched via the API on your server
    redirectUrl: "http://my.site.com/redirect",     // (optional) Where to go after the user signed
    allowCancel: true,                              // (optional) Whether to allow the user to cancel i.e. close the iFrame without signing (default is true)
    messageListener: function(eventData) {          // (optional) Called whenever the iFrame is messaging your page
        /*  do something */ 
    }    
});


NOTES:
 - Both create_embedded_with_reusable_form and create_embedded take the same parameters as their non-embedded counterparts (send and send_with_reusable_form).
   See http://www.hellosign.com/api/reference#SignatureRequest for documentation details.
 - Domain restriction
    The iFrame checks that the parent window belongs to the domain associated with your app, the signature page will not show up if this is not the case
 - If a redirect url is specified, the iFrame will redirect users to it after they signed. Data from the EVENT_SIGNED event will be appended to the url query string
 - Signature urls are only valid for 15 minutes after embedded/sign_url has been called and expire as soon as they're accessed
 - Client side event data is formatted as { "event": "EVENT_NAME", ... }
 - Client side events:
    HelloSign.EVENT_SIGNED      The user has signed, eventData contains a 'signature_id' field
    HelloSign.EVENT_CANCELED    The user has canceled before signing the document
    HelloSign.EVENT_ERROR       An error ocurred, eventData contains a 'description' field


LIVE DEMOS:
 - https://www.hellofax.com/info/testEmbedded
   Embedded signing on Hellofax, signature request for one signer from a test file.
   Once the signer has signed, it automatically closes the iFrame.
 - https://www.hellofax.com/info/testEmbedded2
   Same, but from a reusable form with two signers. 
   Once the first one has signed, it automatically takes you to the signature page for the second one. 
   The two signature would normally not be done within the same session but this illustrate the flow for more than one signer.