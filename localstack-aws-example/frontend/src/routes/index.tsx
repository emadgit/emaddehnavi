import { component$, $, useSignal, useComputed$ } from "@builder.io/qwik";
import type { DocumentHead } from "@builder.io/qwik-city";

export default component$(() => {
  const inputFile = useSignal<HTMLInputElement>();
  const userInput = useSignal("");
  const downloadedImage = useSignal<string | null>(null);

  const uploadFile = $(async () => {
    if (!inputFile.value?.files || inputFile.value.files.length === 0) {
      alert("Please select a file first.");
      return;
    }

    const file = inputFile.value.files[0];
    const formData = new FormData();
    formData.append("MyFile", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        alert("File uploaded successfully!");
      } else {
        alert(`File upload failed: ${response.statusText}`);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  });

  const fileName = useComputed$(() => userInput.value);

  const handleDownload = $(async () => {
    if (!fileName.value) {
      alert("Please enter a file name to download.");
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/download/${fileName.value}`,
        {
          method: "GET",
        },
      );

      if (!response.ok) {
        alert(`Failed to download file: ${response.statusText}`);
        return;
      }

      // Convert response stream to Blob
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      // Save for rendering or downloading
      downloadedImage.value = url;
    } catch (error) {
      console.error("Error downloading file:", error);
    }
  });

  return (
    <>
      <div class="flex max-h-full w-1/2 flex-col items-center justify-center gap-4 p-4 text-gray-100">
        <div class="flex flex-row gap-4">
          <input type="file" ref={inputFile} />
          <div class="flex flex-row items-start justify-start gap-4">
            <button
              class="w-fit bg-gray-600 p-2 text-stone-100"
              onClick$={uploadFile}
            >
              Upload
            </button>
          </div>
        </div>
        <div class="flex w-1/2 flex-col text-slate-50">
          <hr />
        </div>
        <div class="flex flex-col gap-4">
          <div class="flex w-1/2 flex-row gap-2 text-slate-50">
            <input
              type="text"
              bind:value={userInput}
              class="p-2 text-yellow-950"
            />
            <button
              class="w-fit bg-gray-600 p-2 text-stone-100"
              onClick$={handleDownload}
            >
              Download
            </button>
          </div>
          <p>{fileName.value && `What file to download: ${fileName.value}`}</p>
        </div>
        {downloadedImage.value && (
          <div class="flex flex-col items-center gap-4">
            <p>Downloaded Image:</p>
            <img
              src={downloadedImage.value}
              width={150}
              height={150}
              alt="Downloaded file"
              class="max-h-64 max-w-full"
            />
            <a
              href={downloadedImage.value}
              download={fileName.value}
              class="w-fit bg-blue-600 p-2 text-white"
            >
              Save File
            </a>
          </div>
        )}
      </div>
    </>
  );
});

export const head: DocumentHead = {
  title: "Localstack example",
  meta: [
    {
      name: "description",
      content:
        "A simple frontend to upload and download files from an AWS S3 bucket locally using Localstack",
    },
  ],
};
