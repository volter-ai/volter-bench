import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  description?: string
  stats?: string
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ className, uid, description, stats, children, ...props }, ref) => {
    return (
      <HoverCard>
        <HoverCardTrigger asChild>
          <Button
            ref={ref}
            className={cn("w-[200px]", className)}
            uid={`${uid}-button`}
            {...props}
          >
            {children}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent className="w-80">
          <div className="space-y-2">
            <p className="text-sm">{description}</p>
            <p className="text-sm text-muted-foreground">{stats}</p>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

export { SkillButton }
