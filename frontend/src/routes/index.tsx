import * as React from "react";
import { createFileRoute } from "@tanstack/react-router";
import { Upload } from "@/components/teacher/upload/Upload";
import { Title } from "@/components/ui/Title";

export const Route = createFileRoute("/")({
  component: HomeComponent,
});

function HomeComponent() {
  return (
    <div className="p-2">
      <Title />
      <div className="flex flex-col items-center">
        <Upload
          label="Upload an example of an essay you would give 100%"
          content="Upload a .docx file..."
        />
        <Upload
          label="Upload some examples of essays you have provided feedback on"
          content="Upload several .docx files..."
          multiple={true}
        />
      </div>
    </div>
  );
}
