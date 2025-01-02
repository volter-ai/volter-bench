import * as React from "react"
import * as HoverCardPrimitive from "@/components/ui/hover-card"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable.tsx"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Root> {
  uid: string
  skillName: string
  skillDescription: string
  skillStats: string
}

let SkillButton = HoverCardPrimitive.Root

let SkillButtonTrigger = HoverCardPrimitive.Trigger

let SkillButtonContent = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Content>,
  SkillButtonProps
>(({ className, skillName, skillDescription, skillStats, uid, ...props }, ref) => (
  <HoverCardPrimitive.Content
    ref={ref}
    className={cn(
      "z-50 w-64 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none",
      className
    )}
    data-uid={uid} // Ensure uid is used
    {...props}
  >
    <div>
      <h3 className="font-bold">{skillName}</h3>
      <p>{skillDescription}</p>
      <p className="text-sm text-muted">{skillStats}</p>
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
