$(window).on('load', function() {
  $('[data-ride="steptacular"]').on('finish.lp.steptacular', function(e) {
    var data   = e.formData;
    var lookup = {
      'employees':                'EMP',
      'financing':                'FIN',
      'immigration':              'IMM',
      'incorporation':            'INC',
      'intellectual-property':    'IP',
      'non-disclosure-agreement': 'NDA',
      'other':                    'OTH',
      'privacy-and-terms':        'PRI'
    };
    var $form  = $('form#transaction-form');
    var $input = $form.find('#id_transaction_type');

    var transactions = [];
    $(data['selection']['services']).each(function() {
      if (data['services'] && data['services'][this]) {
        transactions.push(data['services'][this]);
      } else {
        transactions.push(lookup[this]);
      };
    });
    $input.val(transactions);

    $form.submit();
  });
});