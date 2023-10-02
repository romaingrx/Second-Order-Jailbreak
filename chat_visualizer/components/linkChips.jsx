"use client";
import { Chip } from "@nextui-org/react";

export default function AllLinkChips() {
  return (
    <>
      <a
        href="https://github.com/romaingrx/second-order-jailbreak"
        target="_blank"
        rel="noopener noreferrer"
      >
        <Chip label="Code">
            Code
        </Chip>
      </a>
      <a
        href="https://docs.google.com/document/d/1OY5fOWC2_Zf1cCfdAV8PxrL3lwignZi6R_6Mv8vnDoI/export?format=pdf"
        target="_blank"
        rel="noopener noreferrer"
      >
        <Chip label="Report">
            Report
        </Chip>
      </a>
    </>
  );
}
