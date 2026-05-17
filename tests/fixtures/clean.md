# A clean public doc

This document describes a technical decision in standalone terms.

The system uses age encryption for client-side data protection. An earlier
investigation surfaced three candidate libraries; the rationale for picking
this one is in the next section.

## Why age

age was chosen over alternatives because it offers a simple file format,
audited primitives, and broad cross-language support. The decision is
independent of any specific project plan.

## Architecture

Clients encrypt locally; storage is opaque. Sync uses ETag locking to
detect concurrent writes.
