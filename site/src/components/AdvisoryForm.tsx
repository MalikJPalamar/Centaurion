import { useForm, type SubmitHandler } from "react-hook-form";
import { z } from "zod";
import { useState } from "react";

const schema = z.object({
  name: z.string().min(2, "Required").max(120),
  role: z.string().min(2, "Required").max(120),
  company: z.string().min(2, "Required").max(160),
  maturity: z
    .string()
    .refine((v) => /^(0[1-9]|1[01])$/.test(v), "Pick a level"),
  challenge: z.string().min(8, "Tell us briefly").max(280),
});

type FormValues = z.infer<typeof schema>;

const levels = [
  "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
] as const;

export default function AdvisoryForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<FormValues>({
    mode: "onTouched",
  });
  const [status, setStatus] = useState<"idle" | "ok" | "err">("idle");

  const onSubmit: SubmitHandler<FormValues> = async (values) => {
    const parsed = schema.safeParse(values);
    if (!parsed.success) {
      setStatus("err");
      return;
    }
    try {
      const res = await fetch("/api/advisory-request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parsed.data),
      });
      if (!res.ok) throw new Error(String(res.status));
      setStatus("ok");
      reset();
    } catch {
      setStatus("err");
    }
  };

  if (status === "ok") {
    return (
      <div className="hairline bg-carbon p-8 space-y-3">
        <p className="font-mono text-caption uppercase tracking-[0.08em] text-mist">Received</p>
        <h3 className="text-display-3 text-platinum">Reply within 48 hours.</h3>
        <p className="text-body text-mercury">
          Submissions reach the founder directly. No sales sequence.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="grid gap-6" noValidate>
      <Field label="Name" error={errors.name?.message}>
        <input
          {...register("name", { required: true })}
          className="input-hairline"
          autoComplete="name"
        />
      </Field>
      <Field label="Role" error={errors.role?.message}>
        <input
          {...register("role", { required: true })}
          className="input-hairline"
          autoComplete="organization-title"
          placeholder="Chief AI Officer, CTO, …"
        />
      </Field>
      <Field label="Company" error={errors.company?.message}>
        <input
          {...register("company", { required: true })}
          className="input-hairline"
          autoComplete="organization"
        />
      </Field>
      <Field label="Current AI maturity" error={errors.maturity?.message}>
        <select {...register("maturity", { required: true })} className="input-hairline">
          <option value="">Select a level…</option>
          {levels.map((n) => (
            <option key={n} value={n}>Level {n}</option>
          ))}
        </select>
      </Field>
      <Field label="Primary challenge (max 280 chars)" error={errors.challenge?.message}>
        <textarea
          {...register("challenge", { required: true })}
          className="input-hairline min-h-[140px] resize-y"
          maxLength={280}
        />
      </Field>
      <div className="flex items-center gap-4">
        <button type="submit" className="btn-signal" disabled={isSubmitting}>
          {isSubmitting ? "Sending…" : "Send →"}
        </button>
        {status === "err" && (
          <p className="font-mono text-caption uppercase tracking-[0.08em] text-mist">
            Something blocked the request. Try again or email founder@centaurion.me.
          </p>
        )}
      </div>
    </form>
  );
}

function Field({
  label,
  error,
  children,
}: {
  label: string;
  error?: string | undefined;
  children: React.ReactNode;
}) {
  return (
    <label className="grid gap-2">
      <span className="font-mono text-caption uppercase tracking-[0.08em] text-mist">{label}</span>
      {children}
      {error ? (
        <span className="font-mono text-caption uppercase tracking-[0.08em] text-signal-blue">{error}</span>
      ) : null}
    </label>
  );
}
