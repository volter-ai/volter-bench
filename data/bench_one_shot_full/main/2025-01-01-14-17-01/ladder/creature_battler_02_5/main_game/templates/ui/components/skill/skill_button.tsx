import * as React from "react"
import * as HoverCardPrimitive from "@/components/ui/hover-card"

import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable.tsx";

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Root> {
  uid: string;
  description: string;
  stats: string;
}

let SkillButton = HoverCardPrimitive.Root

let SkillButtonTrigger = HoverCardPrimitive.Trigger

let SkillButtonContent = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Content>
>(({ className, description, stats, ...props }, ref) => (
  <HoverCardPrimitive.Content
    ref={ref}
    className={cn(
      "z-50 w-64 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none",
      className
    )}
    {...props}
  >
    <div>
      <p>{description}</p>
      <p>{stats}</p>
    </div>
  </HoverCardPrimitive.Content>
))

// Set display name
SkillButtonContent.displayName = HoverCardPrimitive.Content.displayName

// Apply withClickable
SkillButton = withClickable(SkillButton)
SkillButtonTrigger = withClickable(SkillButtonTrigger)
SkillButtonContent = withClickable(SkillButtonContent)

export { SkillButton, SkillButtonTrigger, SkillButtonContent }
