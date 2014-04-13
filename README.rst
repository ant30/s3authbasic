.. image:: https://travis-ci.org/ant30/s3authbasic.svg?branch=master
  :target: https://travis-ci.org/ant30/s3authbasic

.. image:: https://coveralls.io/repos/ant30/s3authbasic/badge.png?branch=master
  :target: https://coveralls.io/r/ant30/s3authbasic?branch=master

.. contents::

===========
s3authbasic
===========


s3authbasic is a Pyramid application aimed to serve a static websites stored
in Amazon S3 protected by Auth Basic authentication. You need a IAM user with
its credentials and read access on the bucket which contains the static
files.

Amazon Settings
===============

I assumed that you have a protected bucket. To create the IAM user with the
correct permissions you need go to the IAM_ app in the AWS Console

.. _IAM: https://console.aws.amazon.com/s3/home

Click **Users** section and click in the **Creare New User** blue button.

Enter the username you want. It can't contains whitespaces. And click on
**create**

Click on **Download Credential** or write down the credentials info.

Now, we need to add the policy to give read access permissions to the user.

Click in the created user and go to the **permissions** tab below.

Click on the **Attach User Policy**.

Click on **Custom Policy** and in the **Select** button.

Give a policy name, like **s3-reader-policy**.

Copy the follow block in the **Policy Document** box. Please,
replace **protected-html** with your bucket name.

.. code-block:: javascript

   {
       "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "s3:Get*",
            "s3:ListBucket"
          ],
          "Resource": [
            "arn:aws:s3:::protected-html",
            "arn:aws:s3:::protected-html/*"
          ]
        }
      ]
   }


Application deployment
======================

I suggest you to use a virtualenv but I don't use that in this doc.

.. code-block:: bash

   pip install s3authbasic


You need a Pyramid ini settings file. You can find one example_ in the
github reposity in the config-templates directory.

.. _example: https://github.com/ant30/s3authbasic/blob/master/config-templates/development.ini


Configuration
=============

You can config the app by editing the settings file or by using envionment
variables.

If you want to use the file, then the AWS and the user settings are
documented in the file.

The AWS environment variables are like this:

.. code-block:: bash

   export AWS_BUCKET_NAME='bucketname'
   export AWS_SECRET_ACCESS_KEY='12312sdf32'
   export AES_ACCESS_KEY_ID='123123123aaa'

To define users to access the app, the variable should starts with **USER_**.
The user name is the word after the underscore character and shoud be defined
in the correct capitalization. This is, if you want a user called **admin**,
you should create the environment variable USER_admin.

You can setup many users as you need.

The password should be hashed by sha256.

You can get the hash of your password by this command in linux:

.. code-block:: bash

   echo -n thepassword | sha256sum

The environment variable should look like this:

.. code-block:: bash

   export USER_admin='123123123123123123123'


Start the application
=====================

You use the follow command:

.. code-block:: bash

   pserve development.ini

If you are using the default ini file, the application should be
available in the 6543 port. If you are deployed the app in your
own system, you can access it through http://127.0.0.1:6543/
