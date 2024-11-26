import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  description?: string
  stats?: {
    damage?: number
    accuracy?: number
    type?: string
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ className, uid, children, description, stats, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover-card`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            ref={ref}
            uid={`${uid}-button`}
            className={cn("w-full", className)}
            {...props}
          >
            {children}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{children}</h4>
            {description && (
              <p className="text-sm text-muted-foreground">
                {description}
              </p>
            )}
            {stats && (
              <div className="text-sm">
                {stats.damage && <div>Damage: {stats.damage}</div>}
                {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
                {stats.type && <div>Type: {stats.type}</div>}
              </div>
            )}
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
