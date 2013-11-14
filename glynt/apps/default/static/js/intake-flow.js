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
    var selections = data['selection'];

    var $form  = $('form#transaction-form');
    var $intakeData = $form.find('#id_intake_data');
    var $transactionType = $form.find('#id_transaction_type');

    var service = null;
    var transactions = [];
    $(selections['services']).each(function() {
      if (data[this + '-services']) {
        transactions.push(data[this + '-services']);
      } else {
        transactions.push(lookup[this]);
      };
    });
    $transactionType.val(transactions);

    $intakeData.val(JSON.stringify(data));

    $form.submit();
  });

  $('input[type=checkbox], input[type=radio]').on('change', function() {
    var $el    = $(this);
    var $label = $el.closest('label');

    if ($el.attr('type') == 'radio') {
      $('input[name="' + $el.attr('name') + '"]').each(function() {
        $(this).closest('label').removeClass('checked');
      });
    };

    if ($el.is(':checked')) {
      $label.addClass('checked');
    } else {
      $label.removeClass('checked');
    };
  });

});