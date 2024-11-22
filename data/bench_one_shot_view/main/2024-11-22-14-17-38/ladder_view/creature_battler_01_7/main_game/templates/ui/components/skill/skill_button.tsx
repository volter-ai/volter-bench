import * as React from "react"
import * as HoverCardPrimitive from "@radix-ui/react-hover-card"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Root> {
  uid: string
}

let HoverCard = HoverCardPrimitive.Root
let HoverCardTrigger = HoverCardPrimitive.Trigger
let HoverCardContent = React.forwardRef<
  React.ElementRef<typeof HoverCardPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Content>
>(({ className, align = "center", sideOffset = 4, ...props }, ref) => (
  <HoverCardPrimitive.Content
    ref={ref}
    align={align}
    sideOffset={sideOffset}
    className={cn(
      "z-50 w-64 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
      className
    )}
    {...props}
  />
))

HoverCardContent.displayName = HoverCardPrimitive.Content.displayName

// Apply withClickable
HoverCard = withClickable(HoverCard)
HoverCardTrigger = withClickable(HoverCardTrigger)
HoverCardContent = withClickable(HoverCardContent)

export { HoverCard, HoverCardTrigger, HoverCardContent }
export type { SkillButtonProps }
