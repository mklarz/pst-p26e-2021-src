#!/bin/bash
## NOTICE
# Dirty quick script to track "stuff". Buy me a beer :))

# Just quickly print out the current datetime
echo $(date)

## CONSTANTS
SCRIPT_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
SITE_DIR="$SCRIPT_PATH/sites"
CHALLENGES_FILE="$SCRIPT_PATH/challenges.json"
SOLUTIONS_FILE="$SCRIPT_PATH/solutions.json"
CHALLENGE_FILES_DIR="$SCRIPT_PATH/challenge_files"

# Files we want to track, files ending with ".map" will considered as sourcemaps and unpacked.
FILES=(robots.txt humans.txt index.html egg.jpg site.webmanifest global.css build/bundle.css build/bundle.css.map build/bundle.js build/bundle.js.map)

# The domains to monitor
DOMAINS=(p26e.dev beta.p26e.dev)

## FUNCTIONS
download_files() {
  # Download the tracked files from the specified URL
  DOMAIN="$1"
  URL="$2"
  OUTPUT_DIR="$3"
  for FILE in "${FILES[@]}"; do
    TMP_FILE=$(mktemp /tmp/p26e.XXXXXX)
    FILE_URL="$URL/$FILE"
    OUTPUT_PATH="$OUTPUT_DIR/$FILE"
    echo "Downloading: $FILE_URL"
    # Store the file temporary
    wget -q "$FILE_URL" -O "$TMP_FILE"
    FILE_SIZE=$(stat -c%s "$TMP_FILE")

    if [ $FILE_SIZE -ne 0 ]; then
      echo "Successfully downloaded file"
      mv "$TMP_FILE" "$OUTPUT_PATH"
    else
      echo "Downloaded file is 0 bytes, ignoring"
      rm "$TMP_FILE"
    fi
	done
}

unpack_sourcemaps() {
	DOMAIN="$1"
	DOMAIN_DIR="$SITE_DIR/$DOMAIN"
	RELATIVE_OUTPUT_DIR="./sites/$DOMAIN/unpacked"
	ABSOLUTE_OUTPUT_DIR="$DOMAIN_DIR/unpacked"

  # Unpack each sourcemap, delete the old unpacked files first
  for FILE in $DOMAIN_DIR/files/build/*.map; do
    if [[ $FILE == *"css"* ]]; then
      rm -rf "$ABSOLUTE_OUTPUT_DIR/css"
      OUTPUT_DIR="$RELATIVE_OUTPUT_DIR/css"
    else
      rm -rf "$ABSOLUTE_OUTPUT_DIR/js"
      OUTPUT_DIR="$RELATIVE_OUTPUT_DIR/js"
    fi

    echo "Unpacking file: $FILE"

    # source-map-unpack, best alternative atm.
    # This tool also messes with paths, removing the first characters of each root file
    # Fixed by:
    # - editing source-map-unpack/dist/index.js (see source-map-unpack/index.js in this repo)
    # - running npx patch-package
    # In addition, it requires relative paths
    # Another alternative is python: unwebpack-sourcemap, albeit more messy
    /usr/local/bin/unpack "$OUTPUT_DIR" "$FILE"
  done
}

fetch_challenges() {
  echo "Looking for new challenges in the API"
  CHALLENGES_TMP_FILE=$(mktemp /tmp/p26e.XXXXXX)
  curl -s https://p26e.dev/api/challenges > "$CHALLENGES_TMP_FILE"
  CURRENT_CHALLENGES_HASH=$(cat $CHALLENGES_FILE | jq . | md5sum | cut -d ' ' -f 1)
  NEW_CHALLENGES_HASH=$(cat $CHALLENGES_TMP_FILE | jq 'map(del(.solutions))' | md5sum | cut -d ' ' -f 1)
  echo "Current challenges hash: $CURRENT_CHALLENGES_HASH, new challenges hash: $NEW_CHALLENGES_HASH"

  if [[ "$CURRENT_CHALLENGES_HASH" != "$NEW_CHALLENGES_HASH" ]]; then
    # We have a diff! Let's handle it

    # Download the image
    IMAGES=$(cat $CHALLENGES_TMP_FILE | jq -r '.[] | select(.image != null) as $p | "\($p._id),\(.image.url)"')
    while IFS= read -r line; do
      # _id, image_url
      IFS=',' read -r -a SPLIT <<< "$line"
      CHALLENGE_ID="${SPLIT[0]}"
      CHALLENGE_DIR="$CHALLENGE_FILES_DIR/$CHALLENGE_ID"
      OUTPUT_PATH="$CHALLENGE_DIR/image.png"
      IMAGE_URL="${SPLIT[1]}"
      mkdir -p "$CHALLENGE_DIR"

      echo "Downloading image for challenge ID $CHALLENGE_ID: $IMAGE_URL"

      # Temporary store the file
      TMP_FILE=$(mktemp /tmp/p26e.XXXXXX)
      wget -q "$IMAGE_URL" -O "$TMP_FILE"
      FILE_SIZE=$(stat -c%s "$TMP_FILE")

      if [ $FILE_SIZE -ne 0 ]; then
	echo "Successfully downloaded file"
        mv "$TMP_FILE" "$OUTPUT_PATH"
      else
	echo "Downloaded file is 0 bytes, ignoring"
        rm "$TMP_FILE"
      fi
    done <<< "$IMAGES"

    # Let's download all the attachments that are specified in the challenges
    ATTACHMENTS=$(cat $CHALLENGES_TMP_FILE | jq -r '.[] | select(.attachments != null) as $p | .attachments[] | "\($p._id),\(.filename),\(.url)"')
    while IFS= read -r line; do
      echo "$line"
      # _id, attachment_filename, attachment_url
      IFS=',' read -r -a SPLIT <<< "$line"
      CHALLENGE_ID="${SPLIT[0]}"
      CHALLENGE_DIR="$CHALLENGE_FILES_DIR/$CHALLENGE_ID"
      ATTACHMENT_FILENAME="${SPLIT[1]}"
      ATTACHMENT_URL="${SPLIT[2]}"
      OUTPUT_PATH="$CHALLENGE_DIR/$ATTACHMENT_FILENAME"
      mkdir -p "$CHALLENGE_DIR"


      echo "Downloading attachment ($ATTACHMENT_FILENAME) for challenge ID $CHALLENGE_ID: $ATTACHMENT_URL"

      # Temporary store the file
      TMP_FILE=$(mktemp /tmp/p26e.XXXXXX)
      wget -q "$ATTACHMENT_URL" -O "$TMP_FILE"
      FILE_SIZE=$(stat -c%s "$TMP_FILE")

      if [ $FILE_SIZE -ne 0 ]; then
	echo "Successfully downloaded file"
        mv "$TMP_FILE" "$OUTPUT_PATH"
      else
	echo "Downloaded file is 0 bytes, ignoring"
        rm "$TMP_FILE"
      fi
    done <<< "$ATTACHMENTS"

    # Seperate the challenges and solutions, easier for viewing diffs
    cat $CHALLENGES_TMP_FILE | jq 'map(del(.solutions))' > $CHALLENGES_FILE
    cat $CHALLENGES_TMP_FILE | jq 'map({_id, title, solutions})' > $SOLUTIONS_FILE

    rm "$CHALLENGES_TMP_FILE"

    echo "There are challenge differences, comitting!"
    commit_diff "New changes to challenges"
  else
    echo "No challenge differences"
  fi

}

commit_diff() {
  # Commit the changes
  COMMIT_MESSAGE="$1"
  echo "Committing with message: $COMMIT_MESSAGE"
  git add -A
  git commit -m "$COMMIT_MESSAGE"
}

handle_diff() {
  DOMAIN="$1"
  COMMIT_MESSAGE="$2"
  DOMAIN_DIR="$SITE_DIR/$DOMAIN"

  # Check sourcemaps
  unpack_sourcemaps "$DOMAIN"

  # Commit the differences
  commit_diff "$COMMIT_MESSAGE"
}

check_domain() {
  DOMAIN="$1"
  URL="https://$DOMAIN"
  echo "Checking $DOMAIN"
  DOMAIN_DIR="$SITE_DIR/$DOMAIN" 
  # Create directories if missing
  mkdir -p "$DOMAIN_DIR/unpacked/js"
  mkdir -p "$DOMAIN_DIR/unpacked/css"
  mkdir -p "$DOMAIN_DIR/files/build"

  COMMIT_MESSAGE="[$DOMAIN] Files were updated"
  # Let's download all the files we track
  download_files "$DOMAIN" "$URL" "$DOMAIN_DIR/files"


  if [[ `git status --porcelain` ]]; then
    # We have a diff! Let's handle it
    echo "There are differences, checking..."
    handle_diff "$DOMAIN" "$COMMIT_MESSAGE"
  else
    echo "No differences"
  fi
}

## GOGO
echo "Starting script..."

# Initialize stuff
mkdir -p $SITE_DIR

cd $SCRIPT_PATH # dirty

# Handle each domain
for DOMAIN in "${DOMAINS[@]}"; do
  check_domain "$DOMAIN"
done

# Check if there are new challenges from the API
fetch_challenges

# Push changes (if any)
git push origin main
