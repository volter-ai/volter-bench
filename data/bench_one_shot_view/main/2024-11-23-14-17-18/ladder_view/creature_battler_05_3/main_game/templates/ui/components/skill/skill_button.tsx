import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/custom/hover-card"
import { Button } from "@/components/ui/custom/button"
import { cn } from "@/lib/utils"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  description?: string
  stats?: {
    power?: number
    accuracy?: number
    cost?: number
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ className, uid, children, description, stats, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            uid={`${uid}-button`}
            ref={ref}
            className={cn("w-[200px]", className)}
            {...props}
          >
            {children}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <p className="text-sm">{description}</p>
            {stats && (
              <div className="text-xs text-muted-foreground">
                {stats.power && <div>Power: {stats.power}</div>}
                {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
                {stats.cost && <div>Cost: {stats.cost}</div>}
              </div>
            )}
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

export { SkillButton }
