import * as React from "react"
import * as HoverCardPrimitive from "@/components/ui/hover-card"

import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable.tsx";

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Trigger> {
  uid: string;
  description: string;
  stats: string;
}

let SkillButton = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Trigger>,
  SkillButtonProps
>(({ className, description, stats, uid, ...props }, ref) => (
  <HoverCardPrimitive.Root>
    <HoverCardPrimitive.Trigger
      ref={ref}
      className={cn("skill-button", className)}
      {...props}
    />
    <HoverCardPrimitive.Content>
      <div className="tooltip-content">
        <p>{description}</p>
        <p>{stats}</p>
      </div>
    </HoverCardPrimitive.Content>
  </HoverCardPrimitive.Root>
))

// Set display name
SkillButton.displayName = "SkillButton"

// Apply withClickable
SkillButton = withClickable(SkillButton)

export { SkillButton }
