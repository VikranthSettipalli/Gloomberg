// Common UI components - placeholders

export function Loading() {
  return <div>Loading...</div>;
}

export function ErrorMessage({ message }: { message: string }) {
  return <div style={{ color: 'red' }}>Error: {message}</div>;
}
