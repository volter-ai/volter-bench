import * as React from "react"
import * as HoverCardPrimitive from "@radix-ui/react-hover-card"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Root> {
  uid: string
}

let SkillButton = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Root>,
  SkillButtonProps
>(({ className, uid, ...props }, ref) => (
  <HoverCardPrimitive.Root
    ref={ref}
    className={cn(className)}
    {...props}
  />
))

SkillButton.displayName = HoverCardPrimitive.Root.displayName

// Apply withClickable
SkillButton = withClickable(SkillButton)

export { SkillButton }
