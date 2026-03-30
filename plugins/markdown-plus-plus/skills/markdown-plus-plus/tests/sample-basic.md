# Basic Markdown++ Sample

This file demonstrates basic Markdown++ extensions for testing.

## Variables

Welcome to $product_name;, version $version;.

The **$product_name;** application is available for download at $download_url;.

## Custom Styles

<!--style:Heading1-->
# Styled Heading

<!--style:ImportantNote-->
> This is an important note with a custom style.

This text includes <!--style:Emphasis-->**emphasized content** inline.

## Custom Aliases

<!--#introduction-->
## Introduction

This section has a custom alias for linking.

See [Introduction](#introduction) for more details.

## Conditions

<!--condition:web-->
This content appears only in web output.
<!--/condition-->

<!--condition:print-->
This content appears only in print output.
<!--/condition-->

<!--condition:!internal-->
This content appears when "internal" is NOT set.
<!--/condition-->

## Markers

<!--marker:TopicAlias="TopicID"-->
This paragraph has associated keywords.

<!--marker:IndexMarker="fruit"-->
This paragraph has an associated index term for "apple".

## Simple Table

| Feature | Status |
|---------|--------|
| Variables | Supported |
| Styles | Supported |
| Conditions | Supported |
