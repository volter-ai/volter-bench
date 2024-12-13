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
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={className} {...props} />
  )
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let BaseCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} {...props} />
  )
)

let BaseCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

let BaseProgress = React.forwardRef<HTMLDivElement, BaseCardProps & { value: number }>(
  ({ className, uid, ...props }, ref) => (
    <Progress ref={ref} className={className} {...props} />
  )
)

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardTitle = withClickable(BaseCardTitle)
BaseCardContent = withClickable(BaseCardContent)
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
