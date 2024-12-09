import * as React from "react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import * as HoverCardPrimitive from "@radix-ui/react-hover-card"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  skillName: string
  description: string
  stats: string
}

let HoverCard = HoverCardPrimitive.Root
let HoverCardTrigger = HoverCardPrimitive.Trigger
let HoverCardContent = HoverCardPrimitive.Content
let BaseButton = Button

// Apply withClickable
HoverCard = withClickable(HoverCard)
HoverCardTrigger = withClickable(HoverCardTrigger)
HoverCardContent = withClickable(HoverCardContent)
BaseButton = withClickable(BaseButton)

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, className, skillName, description, stats, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger uid={uid}>
          <BaseButton
            ref={ref}
            className={cn("w-[200px]", className)}
            uid={uid}
            {...props}
          >
            {skillName}
          </BaseButton>
        </HoverCardTrigger>
        <HoverCardContent uid={uid} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm text-muted-foreground">
              {description}
            </p>
            <div className="text-sm text-muted-foreground">
              {stats}
            </div>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

export { SkillButton }
