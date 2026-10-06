<?php

// Find our position in the file tree
if (!defined('DOCROOT')) {
    $docroot = get_cfg_var('doc_root');
    define('DOCROOT', $docroot);
}

/************* Agent Authentication ***************/

// Set up and call the AgentAuthenticator
require_once (DOCROOT . '/include/services/AgentAuthenticator.phph');

// On failure, this will print out 'Access Denied', then exit, preventing the page from proceeding.
$account = AgentAuthenticator::AuthenticateBatchJob();
/********************* end agent authentication ***************************/
// Set up namespace for CPHP.
use RightNow\Connect\v1 as RNCPHP;

$ip_dbreq = true;
require_once('include/init.phph');
require_once('include/src/rnwintf.phph');

list ($rnw_ui_cfgid, $rnw_common_cfgid) = msg_init($p_cfgdir, 'config', array('rnw_ui', 'rnw_common'));
list ($common_mbid, $rnw_mbid) = msg_init($p_cfgdir, 'msgbase', array('common', 'rnw'));

try {
  // So we need to figure out directly, how to query custom fields from this method. It's not clear.
  // You can't use date_add with functions, I guess???
  $now = date('Y-m-d H:i:s');

  $date1 = new DateTime();
  // The scrub used to be 89 days ago, now 450 days
  $eightynine_days_ago = new DateInterval( "P450D" );
  $eightynine_days_ago->invert = 1; //Make it negative.
  $date1->add( $eightynine_days_ago ); //-89 days.
  $major_update_time = gmdate( 'Y-m-d\TH:i:s\Z', $date1->getTimestamp() );

  $roql_where = 'c$pii_removed = 0 and ID != 1102';
  $roql_where .= sprintf( " and CreatedTime <= '%s'", $major_update_time );
  $contacts = RNCPHP\Contact::find( $roql_where );

  foreach( $contacts as $contact ) {
    // for each $contact, we want to wipe the following fields as prescribed in the TDD:
    $c_id = intval( $contact->ID );
    $contact->Name->First = "Contact ";
    $contact->Name->Last = $c_id;

    $contact->Address->Street = "";
    $contact->Address->City = "";
    $contact->Address->Country = null;
    $contact->Address->StateOrProvince = null;

    // Loop through the email addresses and wipe all of
    //  them. This works and saves.
    foreach( $contact->Emails as $k => $email ) {
      // The following commented out lines are FYIs.
      $contact->Emails[ intval($k) ]->Address = "Contact.$c_id.$k@cancer.gov.invalid";
      $contact->Emails[ intval($k) ]->Invalid = true; //Invalid it.
    }

    // Though not what was originally planned, using
    //  an all 5 phone number works. Therefore, proceeding
    //  with this as it acheives the goal.
    foreach( $contact->Phones as $k => $phone ) {
      $contact->Phones[ intval($k) ]->Number = "555-555-5555"; //Just try to replace each number to an all five number.
    }

    $contact->CustomFields->pii_removed = true;

    $contact->save();
  }
  RNCPHP\ConnectAPI::commit();
} catch (RNCPHP\ConnectAPIError $err)  {
  echo "An error has occured.\nMessage: ".$err->getMessage();
  print "\nCode: ". $err->getCode();
}
