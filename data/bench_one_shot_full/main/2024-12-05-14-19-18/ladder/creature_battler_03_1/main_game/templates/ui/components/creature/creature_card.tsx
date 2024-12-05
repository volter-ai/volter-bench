import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("rounded-xl border bg-card text-card-foreground shadow", className)}
      {...props}
    />
  )
)

let CardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex flex-col space-y-1.5 p-6", className)}
      {...props}
    />
  )
)

let CardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps & React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, uid, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn("font-semibold leading-none tracking-tight", className)}
      {...props}
    />
  )
)

let CardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
  )
)

Card.displayName = "Card"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"
CardContent.displayName = "CardContent"

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardContent = withClickable(CardContent)

interface CreatureCardProps extends BaseCardProps {
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
        <CardHeader uid={uid}>
          <CardTitle uid={uid}>{name}</CardTitle>
          <div className="h-4 w-full bg-gray-200 rounded-full">
            <div 
              className="h-4 bg-green-500 rounded-full" 
              style={{width: `${(hp/maxHp) * 100}%`}}
            />
          </div>
          <div className="text-sm text-right">{`${hp}/${maxHp}`}</div>
        </CardHeader>
        <CardContent uid={uid}>
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-contain"
          />
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
