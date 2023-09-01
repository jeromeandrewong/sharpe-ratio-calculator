"use client";

import React from "react";
import { Card, CardBody } from "@nextui-org/react";

export default function App({ children }: { children: React.ReactNode }) {
  return (
    <Card>
      <CardBody>{children}</CardBody>
    </Card>
  );
}
