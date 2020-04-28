#!/usr/bin/env bash

rm LUTHER

cd src
zip -r ../LUTHER.zip *
cd ..
echo '#!/usr/bin/env python3' | cat - LUTHER.zip > LUTHER
rm LUTHER.zip

chmod 755 LUTHER
