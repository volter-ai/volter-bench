import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

interface WrappedCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let WrappedCard = React.forwardRef<HTMLDivElement, WrappedCardProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let WrappedCardContent = React.forwardRef<HTMLDivElement, WrappedCardProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let WrappedCardHeader = React.forwardRef<HTMLDivElement, WrappedCardProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let WrappedCardTitle = React.forwardRef<HTMLParagraphElement, WrappedCardProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let WrappedProgress = React.forwardRef<HTMLDivElement, WrappedCardProps & { value: number }>(
  ({ uid, ...props }, ref) => <Progress ref={ref} {...props} />
)

WrappedCard = withClickable(WrappedCard)
WrappedCardContent = withClickable(WrappedCardContent)
WrappedCardHeader = withClickable(WrappedCardHeader)
WrappedCardTitle = withClickable(WrappedCardTitle)
WrappedProgress = withClickable(WrappedProgress)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    const hpPercentage = (currentHp / maxHp) * 100

    return (
      <WrappedCard ref={ref} uid={uid} className={cn("w-[300px]", className)} {...props}>
        <WrappedCardHeader uid={`${uid}-header`}>
          <WrappedCardTitle uid={`${uid}-title`}>{name}</WrappedCardTitle>
        </WrappedCardHeader>
        <WrappedCardContent uid={`${uid}-content`}>
          <div className="relative aspect-square w-full mb-4">
            <img
              src={image}
              alt={name}
              className="object-contain w-full h-full"
            />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{`${currentHp}/${maxHp}`}</span>
            </div>
            <WrappedProgress uid={`${uid}-progress`} value={hpPercentage} />
          </div>
        </WrappedCardContent>
      </WrappedCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
