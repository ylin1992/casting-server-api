#!/bin/bash
export DEV_LEVEL='LOCAL'

export AUTH0_DOMAIN='dev-artpgixt.us.auth0.com'
export API_AUDIENCE='casting-api'
export CLIENT_ID='vrDoSPpPqVtxnIRlOQDk7FH8UJsTSPLB'

export TEST_ASSISTANT_TOKEN='<ASSISTANT_TOKEN>'
export TEST_DIRECTOR_TOKEN='<DIRECTOR_TOKEN>'
export TEST_PRODUCER_TOKEN='<PRODUCER_TOKEN>'
export DB_HOST='<YOUR_SECRET_DB_HOST_NAME>'
export DB_USER='<YOUR_USER_NAME>'
export DB_PWD='<YOUR_DB_PWD>'
export DB_NAME='casting'
export DB_TEST_NAME='casting_test' 

createdb casting_test
psql -d casting_test -h 127.0.0.1 -U $DB_USER --echo-all -f ./database/create_test_tables.sql