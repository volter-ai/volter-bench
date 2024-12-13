import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let GameCard = withClickable(React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={className} {...props} />
  )
))

let GameCardContent = withClickable(React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
))

let GameCardHeader = withClickable(React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
))

let GameCardTitle = withClickable(React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} {...props} />
  )
))

let GameProgress = withClickable(React.forwardRef<HTMLDivElement, BaseCardProps & { value: number }>(
  ({ className, uid, ...props }, ref) => (
    <Progress ref={ref} className={className} {...props} />
  )
))

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  currentHp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, currentHp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <GameCard uid={`${uid}-card`} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <GameCardHeader uid={`${uid}-header`}>
          <GameCardTitle uid={`${uid}-title`}>{name}</GameCardTitle>
        </GameCardHeader>
        <GameCardContent uid={`${uid}-content`} className="flex flex-col gap-4">
          <img
            src={imageUrl}
            alt={name}
            className="aspect-square w-full object-cover"
          />
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{`${currentHp}/${maxHp}`}</span>
            </div>
            <GameProgress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
          </div>
        </GameCardContent>
      </GameCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
