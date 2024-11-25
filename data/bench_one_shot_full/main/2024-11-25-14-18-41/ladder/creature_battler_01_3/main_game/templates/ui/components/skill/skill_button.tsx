import * as React from "react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import * as HoverCardPrimitive from "@radix-ui/react-hover-card"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  description: string
  stats: string
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
let WrappedButton = withClickable(Button)

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ className, uid, description, stats, children, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger uid={uid} asChild>
          <WrappedButton
            uid={uid}
            ref={ref}
            className={cn("w-[200px]", className)}
            {...props}
          >
            {children}
          </WrappedButton>
        </HoverCardTrigger>
        <HoverCardContent uid={uid} className="w-80">
          <div className="space-y-2">
            <p className="text-sm">{description}</p>
            <p className="text-sm font-mono">{stats}</p>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

export { SkillButton }
