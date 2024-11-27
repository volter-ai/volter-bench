import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface CreatureCardProps extends BaseCardProps {
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let BaseCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let BaseCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let BaseCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let BaseProgress = React.forwardRef<HTMLDivElement, BaseCardProps & { value: number }>(
  ({ uid, ...props }, ref) => <Progress ref={ref} {...props} />
)

BaseCard.displayName = "BaseCard"
BaseCardContent.displayName = "BaseCardContent"
BaseCardHeader.displayName = "BaseCardHeader"
BaseCardTitle.displayName = "BaseCardTitle"
BaseProgress.displayName = "BaseProgress"

BaseCard = withClickable(BaseCard)
BaseCardContent = withClickable(BaseCardContent)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardTitle = withClickable(BaseCardTitle)
BaseProgress = withClickable(BaseProgress)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <BaseCard ref={ref} uid={uid} className={cn("w-[300px]", className)} {...props}>
        <BaseCardHeader uid={uid}>
          <BaseCardTitle uid={uid}>{name}</BaseCardTitle>
        </BaseCardHeader>
        <BaseCardContent uid={uid} className="flex flex-col gap-4">
          <img 
            src={image}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{currentHp}/{maxHp}</span>
            </div>
            <BaseProgress uid={uid} value={(currentHp / maxHp) * 100} />
          </div>
        </BaseCardContent>
      </BaseCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
